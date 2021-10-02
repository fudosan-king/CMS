import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'cafe_aqua': {
                name : translator.t('Cafe aqua'),
                uri: require('./cafe-aqua.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#D6DFCE'
            }   
        };
    },
};