import {resolve} from 'path'
import {defineConfig} from 'vite'
import commonjs from '@rollup/plugin-commonjs';
import {babel} from '@rollup/plugin-babel';
import terser from '@rollup/plugin-terser';
import vue from '@vitejs/plugin-vue'
import { splitVendorChunkPlugin } from 'vite'

export default defineConfig(({mode}) => {
    return {
        // mode: 'development',
        plugins: [vue(), commonjs(), babel({babelHelpers: 'bundled'}), mode === "dev" ? "" : terser(), splitVendorChunkPlugin()],
        define: {
            'process.env.NODE_ENV': JSON.stringify(mode),
        },
        resolve: {
            alias: {
                vue: 'vue/dist/vue.esm-bundler.js',
            },
        },
        build: {
            emptyOutDir: false,
            minify: mode === "dev" ? false : 'terser',
            target: 'es2015',
            lib: {
                formats: ['iife'],
                name: 'Spark2',
                entry: resolve(__dirname, 'src/app.ts'),
            },
            commonjsOptions: {
                include: [/node_modules/]
            },
            outDir: './static',
            rollupOptions: {

                // external: ['vue'],

                output: {
                    // inlineDynamicImports: false,
                    // manualChunks: (id) => {
                    //     if (id.includes('node_modules')) {
                    //         return 'vendors';
                    //     }
                    // },

                    // globals: {
                    //     vue: 'Vue',
                    // },
                    entryFileNames: mode === "dev" ? 'js/main.js' : 'js/main.min.js',
                    chunkFileNames: mode === "dev" ? 'js/[name].js' : 'js/[name].min.js',
                    assetFileNames: mode === "dev" ? '[ext]/[name].[ext]' : '[ext]/[name].min.[ext]',
                }
            }
        }
    }
})