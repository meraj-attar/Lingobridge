import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'./e2e', use:{baseURL:'http://localhost:5175',headless:true},timeout:25000,reporter:'list'});
