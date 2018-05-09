const resolve = require('path').resolve
const webpack = require('webpack')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const url = require('url')
const publicPath = ''

module.exports = (options = {}) => ({
  entry: {
    //vendor: ["babel-polyfill", './src/vendor'],
    index:  './src/main.js'
  },
  output: {
    path: resolve(__dirname, 'dist'),
    filename: options.dev ? '[name].js' : '[name].js?[chunkhash]',
    chunkFilename: '[id].js?[chunkhash]',
    publicPath: options.dev ? '/assets/' : publicPath
  },
  module: {
    rules: [{
        test: /\.vue$/,
        use: ['vue-loader']
      },
      {
        test: /\.js$/,
        use: ['babel-loader'],
        exclude: /node_modules/
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader', 'postcss-loader']
      },
      {
        test: /\.(png|jpg|jpeg|gif|eot|ttf|woff|woff2|svg|svgz)(\?.+)?$/,
        use: [{
          loader: 'url-loader',
          options: {
            limit: 10000
          }
        }]
      }
    ]
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin({
      names: ['vendor', 'manifest']
    }),
    new HtmlWebpackPlugin({
      template: 'src/index.html'
    }),
	new webpack.NormalModuleReplacementPlugin(
		/element-ui[\/\\]lib[\/\\]locale[\/\\]lang[\/\\]zh-CN/,
		'element-ui/lib/locale/lang/zh-TW'
	),
	new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
      /*new webpack.optimize.UglifyJsPlugin({
        compress: {
          warnings: false
        }
      })*/
  ],
  resolve: {
        alias: {
            '~': resolve(__dirname, 'src'),
            vue: 'vue/dist/vue.common.js',
        }
  },
  devServer: {
    host: '0.0.0.0',
    port: 8012,
	disableHostCheck: true,
    proxy: {
      '/kong/auth': {
        target: 'http://localhost:8008',
        changeOrigin: true,
        pathRewrite: {
          '^/kong/auth': ''
        }
      },
      '/kong/employeemng': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        pathRewrite: {
          '^/kong': ''
        }
      },
	  '/kong/rightmanage': {
        target: 'http://localhost:8008',
        changeOrigin: true,
        pathRewrite: {
          '^/kong': ''
        }
      },
	  '/kong/gongdi_mng': {
        target: 'http://localhost:8889',
        changeOrigin: true,
        pathRewrite: {
          '^/kong': ''
        }
      },
	  '/kong/': {
		target: 'http://localhost:8899',
		changeOrigin: true,
		pathRewrite: {
		  '^/kong': ''
		}
	  },
    },
	/*proxy: {
	'/kong/': {
        target: 'http://192.168.101.31:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/kong': ''
        }
      }
    },*/
    historyApiFallback: {
      index: url.parse(options.dev ? '/assets/' : publicPath).pathname
    }
  },
  devtool: options.dev ? '#eval-source-map' : '#source-map'
})
