import {resolve} from 'path'
import {defineConfig, loadEnv, splitVendorChunkPlugin} from 'vite'
import commonjs from '@rollup/plugin-commonjs';
import { babel } from '@rollup/plugin-babel';
import vue from '@vitejs/plugin-vue'

export default defineConfig(({mode}) => {
    return {
        // mode: 'development',
        plugins: [vue(), babel({ babelHelpers: 'bundled' })],
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
                formats: ['es'],
                name: 'Spark2',
                entry: resolve(__dirname, 'src/app.ts'),
            },
            commonjsOptions: {
                include: [/node_modules/]
            },
            outDir: './static',
            rollupOptions: {

                output: {
                    manualChunks: (id) => {
                        if (id.includes('node_modules')) {
                            return 'vendors';
                        }
                    },
                    entryFileNames: mode === "dev" ? 'js/main.js' : 'js/main.min.js',
                    chunkFileNames: mode === "dev" ? 'js/[name].js' : 'js/[name].min.js',
                    assetFileNames: mode === "dev" ? '[ext]/[name].[ext]' : '[ext]/[name].min.[ext]',
                },
            }
        }
    }
})