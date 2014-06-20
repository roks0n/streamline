require.config({
    include: ['../bower_components/requirejs/require'],
    paths: {
        'jquery': '../bower_components/jQuery/dist/jquery',
    },
    shim: {
        'jquery': {
            deps: [],
            exports: '$'
        }
    }
});
