const gulp        = require('gulp');
const rimraf      = require('rimraf');
const sass        = require('gulp-sass');
const babel       = require('gulp-babel');
const httpProxy   = require('http-proxy');
const concat      = require('gulp-concat');
const inject      = require('gulp-inject');
const runSequence = require('run-sequence');
const wiredep     = require('wiredep').stream;
const sourceMaps  = require('gulp-sourcemaps');
const browserSync = require('browser-sync').create();

gulp.task('compile:es6', () => {
  return gulp.src('./app/**/*.js')
    .pipe(sourceMaps.init())
    .pipe(babel())
    .pipe(sourceMaps.write('.'))
    .pipe(gulp.dest('./dist/app'));
});

gulp.task('compile:sass', () => {
  return gulp.src('./app/app.sass')
    .pipe(sourceMaps.init())
    .pipe(sass().on('error', sass.logError))
    .pipe(sourceMaps.write('.'))
    .pipe(gulp.dest('./dist/app'));
});

gulp.task('compile:react', () => {
  gulp.src('./app/**/*.jsx')
    .pipe(sourceMaps.init())
    .pipe(babel())
    .pipe(concat('react.js'))
    .pipe(sourceMaps.write())
    .pipe(gulp.dest('./dist/app'));
});

gulp.task('compile', ['compile:es6', 'compile:react', 'compile:sass']);

gulp.task('watch:js', () => {
  return gulp.watch('./app/**/*.js', ['compile:es6']);
});

gulp.task('watch:react', () => {
  return gulp.watch('./app/**/*.jsx', ['compile:react']);
});

gulp.task('watch:sass', () => {
  return gulp.watch(['./app/**/*.sass', 'app/app.sass'], ['compile:sass']);
});

gulp.task('watch:html', () => {
  return gulp.watch(['./app/**/*.html'], ['copy:html']);
});

gulp.task('watch:index', () => {
  return gulp.watch(['./index.html'], ['copy:index']);
});

gulp.task('watch', ['watch:js', 'watch:react', 'watch:sass', 'watch:html', 'watch:index']);

gulp.task('inject:js', () => {
  return gulp.src('./index.html')
    .pipe(inject(gulp.src('./app/**/*.js', { read: false })))
    .pipe(gulp.dest('.'))
});

gulp.task('inject:sass', () => {
  return gulp.src('./app/app.sass')
    .pipe(inject(gulp.src(['./app/**/*.sass', '!./app/app.sass'], { read: false }), { relative: true }))
    .pipe(gulp.dest('./app'))
});

gulp.task('inject:vendor', () => {
  return gulp.src('./index.html')
    .pipe(wiredep())
    .pipe(gulp.dest('.'));
});

gulp.task('inject', (cb) => {
  runSequence('inject:sass', 'inject:vendor', 'inject:js', cb);
});

gulp.task('copy:index', () => {
  return gulp.src('./index.html', { read: false }).pipe(gulp.dest('./dist'));
});

gulp.task('copy:assets', () => {
  return gulp.src('./assets/**/*', { read: false }).pipe(gulp.dest('./dist/assets'));
});

gulp.task('copy:html', () => {
  return gulp.src('./app/**/*.html', { read: false }).pipe(gulp.dest('./dist/app'));
});

gulp.task('copy', ['copy:index', 'copy:html', 'copy:assets']);

gulp.task('serve', () => {
  const proxy = httpProxy.createProxyServer({
    target: 'http://localhost:9000/'
  });

  proxy.on('error', function(error, req, res) {
    res.writeHead(500, {
      'Content-Type': 'text/plain'
    });
  });

  browserSync.init({
    server: {
      baseDir: './dist'
    },
    serveStatic: [{
      route: '/bower_components',
      dir: ['./bower_components']
    }],
    files: ['./dist/index.html', './dist/**/*'],
    watchOptions: {
      ignored: '*.map'
    },
    middleware(req, res, next) {
      console.log(`${req.method}: ${req.url}`);

      if (/^\/(api|admin|static)\//.test(req.url)) {
        return proxy.web(req, res);
      } else if (!/\.[a-zA-Z]{1,5}(\/?\?.*)?$/.test(req.url)) {
        req.url = '/';
      }

      return next();
    }
  });
});

gulp.task('clean', (cb) => {
  rimraf('./dist', cb);
});

gulp.task('default', (cb) => {
  runSequence(['clean', 'inject'], ['copy', 'compile'], ['serve', 'watch'], cb);
});
