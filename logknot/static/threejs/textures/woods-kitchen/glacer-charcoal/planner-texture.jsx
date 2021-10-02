import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'glacer_charcoal': {
                name : translator.t('Glacer charcoal'),
                uri: require('./glacer-charcoal.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#888D90'
            }
        };
    },
};