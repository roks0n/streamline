require.config({
    paths: {
        'jquery': '../../bower_components/jQuery/dist/jquery',
    },
    shim: {
        'jquery': {
            deps: [],
            exports: '$'
        }
    }
});
