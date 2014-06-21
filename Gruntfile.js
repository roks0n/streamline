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
                    dir: 'static/js/req/',
                    optimize: 'none',
                    mainConfigFile: 'frontend/requireJSconfig.js',
                    modules: [{
                        name: 'site/main',
                        include: ['require'] // todo: how to make this work on all modules w/o adding it here?
                    }]
                }
            }
        },

        sass: {
            dev: {
                options: {
                    style: 'expanded' //Set your prefered style for development here.
                },
                files: [{
                    expand: true,
                    cwd: 'frontend/css/site/',
                    src: ['*.scss', '*.sass'], // Feel free to remove a format if you do not use it.
                    dest: 'apps/site/static',
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
        'sass',
        'watch'
    ]);

};
