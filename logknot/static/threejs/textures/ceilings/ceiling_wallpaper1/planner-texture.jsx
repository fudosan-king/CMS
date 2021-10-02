export default {
    textureProperties: function (mesh) {
        return {
            ceiling_wallpaper1: {
                name: 'Wallpaper 1',
                uri: require('./wallp-1.jpg'),
                lengthRepeatScale: 0.01,
                heightRepeatScale: 0.01,
                mesh : mesh,
            }
        };
    },
};