import test from 'node:test';
import assert from 'node:assert/strict';
import { extractYouTubeVideoId, getYouTubeEmbedUrl, isValidYouTubeUrl } from '../src/utils/youtube.js';

const id='dQw4w9WgXcQ';
const valid=[
 `https://www.youtube.com/watch?v=${id}`,
 `https://youtu.be/${id}`,
 `https://youtube.com/embed/${id}`,
 `https://youtube.com/shorts/${id}`,
 `https://m.youtube.com/watch?v=${id}&t=30`,
 `https://www.youtube-nocookie.com/embed/${id}`,
 `https://youtube.com/live/${id}`,
];
const invalid=[
 'javascript:alert(1)',`http://youtube.com/watch?v=${id}`,
 `https://youtube.com.evil.example/watch?v=${id}`,
 `https://example.com/youtube.com/watch?v=${id}`,
 `https://youtube.com@evil.example/watch?v=${id}`,
 `https://user:password@youtube.com/watch?v=${id}`,
 `https://youtube.com:443/watch?v=${id}`,
 `https://youtube.com:444/watch?v=${id}`,
 `https://www.youtube.com/watch?v=bad`,
 `https://youtube.com/watch?v=${id}&v=${id}`,
 `https://youtu.be/${id}/extra`,
 `https://youtube.com/`,
 `https://youtube.com/watch?v=${id}#hash`,
 `https://youtube.com\\@evil.example/watch?v=${id}`,
 `https://youtube.com/watch?v=${id}\n`,
 'data:video/mp4;base64,AA==', ' ', null
];
for(const url of valid){
 test(`safe YouTube URL supported: ${url}`,()=>{
   assert.equal(isValidYouTubeUrl(url),true);
   assert.equal(extractYouTubeVideoId(url),id);
   assert.ok(getYouTubeEmbedUrl(url).startsWith('https://www.youtube-nocookie.com/embed/'+id));
 });
}
for(const url of invalid){
 test(`unsafe URL rejected: ${JSON.stringify(url)}`,()=>{
   assert.equal(isValidYouTubeUrl(url),false);
   assert.equal(extractYouTubeVideoId(url),null);
 });
}
test('empty string intentionally clears video',()=>assert.equal(isValidYouTubeUrl(''),true));
test('legacy bare ID still previews but is not a new URL',()=>{
 assert.equal(extractYouTubeVideoId(id),id);
 assert.equal(isValidYouTubeUrl(id),false);
});
