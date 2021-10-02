import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'charcoal': {
                name : translator.t('Charcoal'),
                uri: require('./charcoal.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#6D5C54'
            }
        };
    },
};