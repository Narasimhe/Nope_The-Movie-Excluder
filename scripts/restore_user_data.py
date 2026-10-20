import os
import sqlite3
import struct

def parse_varint(data, offset):
    res = 0
    for i in range(9):
        if offset + i >= len(data):
            return None, offset + i
        b = data[offset + i]
        if i == 8:
            res = (res << 8) | b
            return res, offset + 9
        res = (res << 7) | (b & 0x7F)
        if not (b & 0x80):
            return res, offset + i + 1

def serial_len(st):
    if st == 0: return 0
    if st in (1, 2, 3, 4, 5, 6): return [0, 1, 2, 3, 4, 6, 8][st]
    if st == 7: return 8
    if st in (8, 9): return 0
    if st >= 12 and st % 2 == 0: return (st - 12) // 2
    if st >= 13 and st % 2 == 1: return (st - 13) // 2
    return 0

def restore_database():
    backup_path = 'data/movie_excluder_EMERGENCY_BACKUP.db'
    target_path = 'data/movie_excluder.db'

    if not os.path.exists(backup_path):
        print("Backup file not found:", backup_path)
        return

    with open(backup_path, 'rb') as f:
        raw = f.read()

    PAGE_SIZE = 4096
    VALID_STATUSES = {b'excluded', b'watched', b'watch_later', b'rewatch', b'new_discovery'}

    extracted_user_data = {}

    for p in range(len(raw) // PAGE_SIZE):
        page = raw[p * PAGE_SIZE : (p + 1) * PAGE_SIZE]
        for status_bytes in VALID_STATUSES:
            idx = 0
            while True:
                idx = page.find(status_bytes, idx)
                if idx == -1:
                    break
                
                for h_start in range(max(0, idx - 30), idx):
                    hdr_len, pos = parse_varint(page, h_start)
                    if not hdr_len or pos >= idx or h_start + hdr_len > len(page):
                        continue
                    sts = []
                    cur = pos
                    valid_hdr = True
                    while cur < h_start + hdr_len:
                        st, cur = parse_varint(page, cur)
                        if st is None:
                            valid_hdr = False
                            break
                        sts.append(st)
                    if not valid_hdr or len(sts) < 4:
                        continue
                    
                    body_offset = h_start + hdr_len
                    field_offsets = []
                    for st in sts:
                        field_offsets.append((st, body_offset))
                        body_offset += serial_len(st)
                    
                    match_col = None
                    for col_idx, (st, f_off) in enumerate(field_offsets):
                        if f_off == idx and serial_len(st) == len(status_bytes):
                            match_col = col_idx
                            break
                    
                    if match_col is not None:
                        for c_start in range(max(0, h_start - 12), h_start):
                            plen, r_pos = parse_varint(page, c_start)
                            if not plen or r_pos >= h_start:
                                continue
                            rowid, end_rowid = parse_varint(page, r_pos)
                            if end_rowid == h_start and plen == (body_offset - h_start):
                                vals = []
                                for st, f_off in field_offsets:
                                    length = serial_len(st)
                                    val_bytes = page[f_off : f_off + length]
                                    if st == 0:
                                        vals.append(None)
                                    elif st == 8:
                                        vals.append(0)
                                    elif st == 9:
                                        vals.append(1)
                                    elif st in (1, 2, 3, 4, 5, 6):
                                        vals.append(int.from_bytes(val_bytes, 'big', signed=True))
                                    elif st == 7:
                                        vals.append(struct.unpack('>d', val_bytes)[0])
                                    elif st >= 13 and st % 2 == 1:
                                        vals.append(val_bytes.decode('utf-8', errors='replace'))
                                    else:
                                        vals.append(val_bytes)
                                
                                # If newer record exists, keep the latest updated_at
                                if rowid not in extracted_user_data:
                                    extracted_user_data[rowid] = vals
                                else:
                                    existing_updated = extracted_user_data[rowid][4] if len(extracted_user_data[rowid]) > 4 else ''
                                    new_updated = vals[4] if len(vals) > 4 else ''
                                    if str(new_updated) > str(existing_updated):
                                        extracted_user_data[rowid] = vals
                                break
                idx += len(status_bytes)

    print(f"Extracted {len(extracted_user_data)} user_movie_data records.")

    # Now connect to target DB and insert
    conn = sqlite3.connect(target_path)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = OFF;")

    restored_count = 0
    for tmdb_id, vals in extracted_user_data.items():
        # vals format: [None (rowid), status, verdict, notes, updated_at, is_favorite]
        status = vals[1] if len(vals) > 1 else 'new_discovery'
        verdict = vals[2] if len(vals) > 2 else None
        notes = vals[3] if len(vals) > 3 else None
        updated_at = vals[4] if len(vals) > 4 and vals[4] else 'CURRENT_TIMESTAMP'
        is_favorite = vals[5] if len(vals) > 5 and vals[5] in (0, 1) else 0

        # Ensure a placeholder row in movies exists for FK
        cur.execute(
            "INSERT OR IGNORE INTO movies (tmdb_id, title) VALUES (?, ?)",
            (tmdb_id, f"Movie {tmdb_id}")
        )

        cur.execute(
            """
            INSERT OR REPLACE INTO user_movie_data (tmdb_id, status, verdict, notes, is_favorite, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (tmdb_id, status, verdict, notes, is_favorite, updated_at)
        )
        restored_count += 1

    conn.commit()
    cur.execute("PRAGMA foreign_keys = ON;")
    
    # Check counts
    stats = cur.execute("SELECT status, count(*) FROM user_movie_data GROUP BY status").fetchall()
    print("Database restored successfully!")
    print("Status summary in target database:", stats)
    total = cur.execute("SELECT count(*) FROM user_movie_data").fetchone()[0]
    print(f"Total user movies in target database: {total}")
    conn.close()

if __name__ == "__main__":
    restore_database()
