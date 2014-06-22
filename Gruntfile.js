module.exports = function(grunt) {

    //Initializing the configuration object
    grunt.initConfig({

        // Task configuration
        concat: {
            //...
        },

        uglify: {
            //...
        },


        requirejs: {
            compile: {
                options: {
                    appDir: 'frontend/js/',
                    baseUrl: './',
                    dir: 'compressed/',
                    optimize: 'none',
                    mainConfigFile: 'frontend/requireJSconfig.js',
                    modules: [{
                        // SITE BLUEPRINT
                        name: 'site/main',
                        include: ['../bower_components/requirejs/require']
                    }]
                }
            }
        },

        sass: {
            dev: {
                options: {
                    style: 'expanded', //Set your prefered style for development here.
                    loadPath: [
                        'bower_components/bootstrap-sass-official/vendor/assets/stylesheets/'
                    ],
                },
                files: [{
                    // SITE BLUEPRINT
                    expand: true,
                    cwd: 'frontend/css/site/',
                    src: ['*.scss', '*.sass'], // Feel free to remove a format if you do not use it.
                    dest: 'compressed/site',
                    ext: '.css'
                }]
            }
        },

        watch: {
            css: {
                files: 'frontend/css/{,*/}*.{scss,sass}',
                tasks: ['sass']
            }
        }

    });


    // Plugin loading
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-requirejs');


    // Task definition
    grunt.registerTask('default', [
        'sass:dev',
        'watch'
    ]);

};
