import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'cafe_mocha': {
                name : translator.t('Cafe Mocha'),
                uri: require('./cafe-mocha.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#C9B7A3'
            }   
        };
    },
};