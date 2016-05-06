'use strict';

var gulp        = require('gulp');
var runSequence = require('run-sequence');
var bower       = require('main-bower-files');
var gulpif      = require('gulp-if');
var jshint      = require('gulp-jshint');
var uglify      = require('gulp-uglify');
var concat      = require('gulp-concat');
var flatten     = require('gulp-flatten');
var rename      = require('gulp-rename');
var gulpFilter  = require('gulp-filter');
var nib         = require('nib');
var stylus      = require('gulp-stylus');
var connect     = require('gulp-connect');
var imagemin    = require('gulp-imagemin');
var pngquant    = require('imagemin-pngquant');
var gifsicle    = require('imagemin-gifsicle');
var jpegtran    = require('imagemin-jpegtran');
var svgo        = require('imagemin-svgo');

var DEBUG = process.env.NODE_ENV === 'production' ? false : true;
var dest = '../store/';
var templatesDir = '../store/templates/';
var staticDir = '../store/static/';
// grab libraries files from bower_components, minify and push in /public
gulp.task('bower', function() {
    // var filter = {};
    var jsFilter = gulpFilter('**/*.js', {
        restore: true
    });
    var cssFilter = gulpFilter('**/*.css', {
        restore: true
    });
    var fontFilter = gulpFilter(['*.eot', '*.woff', '*.svg', '*.ttf']);
    var imgFilter = gulpFilter([
        '**/*.png',
        '**/*.jpg',
        '**/*.jpeg',
        '**/*.gif',
        '**/*.svg',
    ], {
        restore: true
    });
    var destPath = staticDir + 'lib';

    return gulp.src(bower({
        debugging: true,
        includeDev: true
    }))

    // grab vendor js files from bower_components, minify and push in /public
    .pipe(jsFilter)
    .pipe(gulp.dest(destPath + '/js/'))
    .pipe(gulpif(!DEBUG, uglify()))
    .pipe(concat('vendor.js'))
    .pipe(rename({
        suffix: '.min'
    }))
    .pipe(gulp.dest(destPath + '/js/'))
    .pipe(jsFilter.restore)

    // grab vendor css files from bower_components, minify and push in /public
    .pipe(cssFilter)
    .pipe(gulp.dest(destPath + '/css/'))
    .pipe(cssFilter.restore)

    // grab vendor img files from bower_components, minify and push in /public
    .pipe(imgFilter)
    .pipe(gulp.dest(destPath + '/images/'))
    .pipe(cssFilter.restore)

    // grab vendor font files from bower_components and push in /public
    .pipe(fontFilter)
    .pipe(flatten())
    .pipe(gulp.dest(destPath + '/fonts/'));
});

gulp.task('browserify', function() {
    return browserify()
    .on('error', gutil.log)
    .require('./src/js/app.js', {
        entry: true,
        extensions: ['.js', 'jsx'],
        debug: true
    })
    .transform(babelify, {
        presets: ['es2015', 'react', 'stage-2']
    })
    .bundle()
    .pipe(source('bundle.js'))
    .pipe(gulp.dest(staticDir + 'js'));
});

gulp.task('js', function() {
    return gulp.src(['src/js/**/*.js', '!src/js/templates/**/*.js'])
    .pipe(jshint({
        devel: DEBUG
    }))
    .pipe(jshint.reporter('jshint-stylish'))
    .pipe(gulpif(!DEBUG,uglify()))
    .pipe(concat('script.js'))
    .pipe(gulp.dest(staticDir + 'js'))
    .pipe(connect.reload());
});

gulp.task('css', function() {
    gulp.src('src/css/style.styl')
    .pipe(stylus({
        use:nib(),
        compress: !DEBUG,
        import:['nib']
    }))
    .pipe(gulp.dest(staticDir + 'css'))
    .pipe(connect.reload());
});

gulp.task('img', function(){
    gulp.src('src/img/**/*')
    .pipe(imagemin({
        progressive: true,
        svgoPlugins: [{removeViewBox: false}],
        use: [pngquant(), gifsicle(), jpegtran(), svgo()]
    }))
    .pipe(gulp.dest(staticDir + 'img'))
    .pipe(connect.reload());
});

gulp.task('html', function() {
    gulp.src('./src/*.html')
    .pipe(gulp.dest(templatesDir))
    .pipe(connect.reload());
});

gulp.task('font', function() {
    gulp.src('./src/font/*')
    .pipe(gulp.dest(staticDir + 'font'))
    .pipe(connect.reload());
});

gulp.task('files', function() {
    gulp.src(['./src/**.*', '!./src/**.*.html', '!./src/**.*js', '!./src/img/'])
    .pipe(gulp.dest(templatesDir));
});

gulp.task('react', function() {
    runSequence('js', 'browserify');
});

gulp.task('connect', function() {
    connect.server({
        root: 'public',
        livereload: true,
    });
});

gulp.task('init', ['css', 'bower', 'react', 'img', 'html', 'files', 'font']);

gulp.task('watch', ['css', 'react', 'img', 'html', 'connect'], function() {
    gulp.watch('src/css/**/*.styl', ['css']);
    gulp.watch('src/js/**/*.js', ['react']);
    gulp.watch('src/js/**/*.jsx', ['react']);
    gulp.watch('src/img/**/*', ['img']);
    gulp.watch('src/*.html', ['html']);
    gulp.watch('src/font/*', ['font']);
});

gulp.task('default', function() {
    runSequence('init', 'watch');
});
