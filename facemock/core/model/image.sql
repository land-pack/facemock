CREATE DATABASE mock;

CREATE TABLE IF NOT EXISTS image2 (
 img_id TEXT PRIMARY KEY, /* image unique id */
 location TEXT NOT NULL, /* //button[.='Yes'] */
 url TEXT NOT NULL,  /* http://localhost:5000/assets/hd/t00001.png */
 status TEXT NOT NULL /* done */);

 CREATE TABLE IF NOT EXISTS image (
  img_id TEXT NOT NULL, /* image unique id */
  location TEXT NOT NULL, /* //button[.='Yes'] */
  url TEXT NOT NULL,  /* http://localhost:5000/assets/hd/t00001.png */
  status TEXT NOT NULL /* done */);
