/**
 * Base webpack config
 */
const path = require('path')
const BundleTracker = require('webpack-bundle-tracker')
const CleanWebpackPlugin = require('clean-webpack-plugin')

// dev-server  port
const PORT = 3000

const paths = {
  root: path.resolve(__dirname),
  buildPath: path.resolve('./static/bundle'),
  appPath: path.resolve('./app'),
  appStyles: path.resolve('./app/styles'),
}

/**
 * app config
 */
const config = (env = {}) => ({
  name: 'app',
  mode: env.production ? 'production' : 'development',
  context: paths.rootPath,

  entry: {
    main: [
      ...(env.devServer ? [`webpack-dev-server/client?http://localhost:${PORT}`] : []), // hmr
      './app/polyfill',
      './app/index',
    ],
  },

  output: {
    path: paths.buildPath,
    filename: env.production ? '[name].[chunkhash:8].js' : '[name].js',
    publicPath: env.devServer ? `http://localhost:${PORT}/bundles/` : '/s/bundle/',
  },

  resolve: {
    extensions: ['.js', '.jsx', '.json'],

    // Allow app imports from '@/some/module'
    alias: {
      '~': paths.appPath,
    },
  },

  module: {
    // Loaders rules for different file types
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            cacheDirectory: true,
          },
        },
      },
      {
        test: /\.s?css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              sourceMap: !env.production,
              minimize: env.production,
            },
          },
          {
            loader: 'sass-loader',
            options: {
              sourceMap: !env.production,
              includePaths: [paths.appStyles],
            },
          },
        ],
      },
      {
        test: /\.svg$/,
        exclude: /node_modules/,
        loader: 'svg-react-loader',
      },
      {
        test: /\.(png|gif|jpg|jpeg)?$/,
        use: 'url-loader',
      },
      {
        test: /\.(ttf|eot|woff|woff2)(\?\S*)?$/,
        use: !env.production ? 'url-loader' : {
          loader: 'file-loader',
          options: {
            name: 'fonts/[hash].[ext]',
          },
        },
      },
    ],
  },

  plugins: [
    // Outputs stats on generated files (used by django-webpack-loader)
    new BundleTracker({ filename: './static/bundle/webpack-stats.json' }),

    // production only
    ...(env.production ? [
    ] : []),

    // dev & production, but not for dev-server
    ...(!env.devServer ? [
      new CleanWebpackPlugin([paths.buildPath], {
        exclude: ['webpack-stats.json'],
        beforeEmit: true,
      }),
    ] : []),
  ],

  optimization: {
    splitChunks: {
      cacheGroups: {
        // vendor.js - node_modules, excluding css modules
        commons: {
          name: 'vendor',
          chunks: 'all',
          test: module => (
            module.context.indexOf('/node_modules/') !== -1 &&
            !/\.s?css$/.test(module.nameForCondition && module.nameForCondition())
          ),
        },
      },
    },
  },

  // production only settings
  ...(env.production ? {
    performance: {
      maxEntrypointSize: 360000,
      maxAssetSize: 300000,
    },
  } : {}),

  // devServer settings
  ...(env.devServer ? {
    devtool: 'inline-cheap-module-eval-source-map',
    devServer: {
      port: PORT,
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    },
  } : {}),
})

module.exports = config
