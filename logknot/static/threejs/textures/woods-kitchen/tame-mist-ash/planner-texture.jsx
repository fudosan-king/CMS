import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'tame_mistAsh': {
                name : translator.t('Mist ash'),
                uri: require('./mist-ash.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#F8F1E1'
            }
        };
    },
};