import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'gash_saxophoneOak': {
                name : translator.t('Gash saxophone oak'),
                uri: require('./gash-saxophone-oak.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#B4BAB8'
            }
        };
    },
};