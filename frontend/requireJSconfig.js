require.config({
    paths: {
        require: '../../bower_components/requirejs/require',
        jquery: '../../bower_components/jQuery/dist/jquery',
    },
    shim: {
        'jquery': {
            deps: [],
            exports: '$'
        }
    }
});
