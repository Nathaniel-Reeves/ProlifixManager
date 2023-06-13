const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    hot: true,
    proxy: {
      '^/': {
        target: 'http://127.0.0.1:8080',
        public: '127.0.0.1:8080'
      },
      '^/api': {
        target: 'http://127.0.0.1:5000'
      }
    }
  }
})
