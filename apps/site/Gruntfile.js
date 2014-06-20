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
                    optimize: "none",
                    baseUrl: "static/",
                    mainConfigFile: "static/requreJSconfig.js",
                    name: "main", // assumes a production build using almond
                    out: "static/optimized.js"
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
                    cwd: 'static/',
                    src: ['*.scss', '*.sass'], // Feel free to remove a format if you do not use it.
                    dest: 'static',
                    ext: '.css'
                }]
            }
        },

        watch: {
            css: {
                files: 'static/{,*/}*.{scss,sass}',
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
