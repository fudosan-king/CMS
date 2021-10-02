import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'gash_ecruMaple': {
                name : translator.t('Gash ecru maple'),
                uri: require('./gash-ecru-maple.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#E7E8EC'
            }
        };
    },
};