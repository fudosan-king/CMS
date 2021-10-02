import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return {
            'color_wood_oak': {
                name : translator.t('Wood oak 1'),
                uri: require('./wood1.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#7C4917'
            }
        };
    },
};