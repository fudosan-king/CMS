import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'cafe_white': {
                name : translator.t('Cafe white'),
                uri: require('./cafe-white.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#E7E7E5'
            }   
        };
    },
};