import {describe,it,expect,vi} from 'vitest';
vi.mock('../src/services/http',()=>({http:{get:vi.fn(),post:vi.fn(),patch:vi.fn(),delete:vi.fn()}}));
import {api} from '../src/services/api';
import {http} from '../src/services/http';
describe('frontend API ownership',()=>{
  it('submits quiz answers only to server scoring',async()=>{
    http.post.mockResolvedValue({percentage:100});
    const result=await api.submitQuiz('lesson-1','client-forged-user',[{question_id:'q',option_id:'o'}]);
    expect(http.post).toHaveBeenCalledWith('/lessons/lesson-1/submit',{answers:[{question_id:'q',option_id:'o'}],attempt_token:null});
    expect(result.percentage).toBe(100);
  });
  it('posts enrollments without trusting a client-specified user id',async()=>{
    http.post.mockResolvedValue({id:'e1'});
    await api.enrollInLanguage('client-forged-user','lang-mr');
    expect(http.post).toHaveBeenCalledWith('/enrollments',{language_id:'lang-mr'});
  });
});
