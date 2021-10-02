import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'glacer_white': {
                name : translator.t('Glacer white'),
                uri: require('./glacer-white.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#F4F5F0'
            }
        };
    },
};