var config = {
   entry: {
       timetable_page: __dirname + "/src/js/index.js",
       signup_page: __dirname + "/src/js/signup.js",
       course_page: __dirname + "/src/js/course.js",
       ripple_effect: __dirname + "/src/js/rippleEffect.js"
   },
   output: {
       path:__dirname + "/dist/js",
       filename: '[name].js',
   },
   devServer: {
       inline: true,
       port: 8080,
       contentBase: "./dist",//本地服务器所加载的页面所在的目录
       historyApiFallback: true,//不跳转
   },
   module: {
       loaders: [
           {
               test: /(\.jsx|\.js)$/,
               exclude: /node_modules/,
               loader: 'babel-loader',
               query: {
                   presets: ['es2015', 'react', 'stage-1'],
                   plugins: ['transform-decorators-legacy','transform-decorators']
               }
           },
           {
               test: /\.css$/, // Only .css files
               loader: 'style-loader!css-loader' // Run both loaders
           },
           {
               test: /\.(png|jpg)$/,
　　　　　　     loader: 'url-loader?limit=12500&name=images/[hash:8].[name].[ext]'
           }
       ]
   }
};
module.exports = config;