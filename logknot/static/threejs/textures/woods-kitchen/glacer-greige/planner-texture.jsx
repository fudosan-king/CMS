import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'glacer_greige': {
                name : translator.t('Glacer greige'),
                uri: require('./glacer-greige.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#A39C82'
            }
        };
    },
};