import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'gash_brassCheek': {
                name : translator.t('Gash brass cheek'),
                uri: require('./gash-brass-cheek.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#E0D7D0'
            }
        };
    },
};