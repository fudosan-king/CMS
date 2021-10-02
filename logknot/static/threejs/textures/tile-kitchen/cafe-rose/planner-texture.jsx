import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'cafe_rose': {
                name : translator.t('Cafe rose'),
                uri: require('./cafe-rose.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#E4DCD9'
            }   
        };
    },
};