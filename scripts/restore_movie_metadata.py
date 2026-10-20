import struct
import sqlite3

def parse_varint(data, offset):
    res = 0
    for i in range(9):
        if offset + i >= len(data): return None, offset + i
        b = data[offset + i]
        if i == 8: return (res << 8) | b, offset + 9
        res = (res << 7) | (b & 0x7F)
        if not (b & 0x80): return res, offset + i + 1

def encode_varint(val):
    if val < 0x80: return bytes([val])
    res = []
    res.append(val & 0x7F)
    val >>= 7
    while val > 0:
        res.append((val & 0x7F) | 0x80)
        val >>= 7
    res.reverse()
    out = []
    for i, b in enumerate(res):
        out.append(b & 0x7F if i == len(res) - 1 else b | 0x80)
    return bytes(out)

def serial_len(st):
    if st == 0: return 0
    if st in (1, 2, 3, 4, 5, 6): return [0, 1, 2, 3, 4, 6, 8][st]
    if st == 7: return 8
    if st in (8, 9): return 0
    if st >= 12 and st % 2 == 0: return (st - 12) // 2
    if st >= 13 and st % 2 == 1: return (st - 13) // 2
    return 0

def restore_movies_metadata():
    conn = sqlite3.connect('data/movie_excluder.db')
    cur = conn.cursor()
    ids = [r[0] for r in cur.execute('SELECT tmdb_id FROM user_movie_data').fetchall()]

    with open('data/movie_excluder_EMERGENCY_BACKUP.db', 'rb') as f:
        raw = f.read()

    restored = 0
    for tmdb_id in ids:
        b_id = encode_varint(tmdb_id)
        idx = 0
        while True:
            idx = raw.find(b_id, idx)
            if idx == -1: break
            h_pos = idx + len(b_id)
            if h_pos < len(raw):
                hdr_len, pos = parse_varint(raw, h_pos)
                if hdr_len and 10 <= hdr_len <= 30 and h_pos + hdr_len <= len(raw):
                    sts = []
                    cur_p = pos
                    valid = True
                    while cur_p < h_pos + hdr_len:
                        st, cur_p = parse_varint(raw, cur_p)
                        if st is None: valid = False; break
                        sts.append(st)
                    if valid and len(sts) >= 10:
                        body_offset = h_pos + hdr_len
                        vals = []
                        for st in sts:
                            l = serial_len(st)
                            v_b = raw[body_offset : body_offset + l]
                            body_offset += l
                            if st == 0: vals.append(None)
                            elif st == 8: vals.append(0)
                            elif st == 9: vals.append(1)
                            elif st in (1, 2, 3, 4, 5, 6): vals.append(int.from_bytes(v_b, 'big', signed=True))
                            elif st == 7: vals.append(struct.unpack('>d', v_b)[0])
                            elif st >= 13 and st % 2 == 1: vals.append(v_b.decode('utf-8', errors='replace'))
                            else: vals.append(v_b)
                        
                        # Check if matches movie schema
                        # vals: [None, title, orig_title, release_date, overview, poster_path, backdrop_path, vote_avg, orig_lang, ...]
                        if len(vals) >= 8 and isinstance(vals[1], str) and len(vals[1]) > 0:
                            title = vals[1]
                            orig_title = vals[2] if len(vals) > 2 and isinstance(vals[2], str) else title
                            release_date = vals[3] if len(vals) > 3 and isinstance(vals[3], str) and '-' in vals[3] else None
                            overview = vals[4] if len(vals) > 4 and isinstance(vals[4], str) else None
                            poster_path = vals[5] if len(vals) > 5 and isinstance(vals[5], str) else None
                            backdrop_path = vals[6] if len(vals) > 6 and isinstance(vals[6], str) else None
                            vote_avg = vals[7] if len(vals) > 7 and isinstance(vals[7], (int, float)) else 0.0
                            orig_lang = vals[8] if len(vals) > 8 and isinstance(vals[8], str) else 'en'

                            cur.execute(
                                """
                                INSERT OR REPLACE INTO movies (
                                    tmdb_id, title, original_title, release_date, overview,
                                    poster_path, backdrop_path, vote_average, original_language
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """,
                                (tmdb_id, title, orig_title, release_date, overview, poster_path, backdrop_path, vote_avg, orig_lang)
                            )
                            restored += 1
                            break
            idx += 1

    conn.commit()
    print(f"Restored metadata for {restored} movies in movies table.")
    real_count = cur.execute("SELECT count(*) FROM movies WHERE title NOT LIKE 'Movie %'").fetchone()[0]
    print(f"Total movies with full metadata in database: {real_count}")
    conn.close()

if __name__ == "__main__":
    restore_movies_metadata()
