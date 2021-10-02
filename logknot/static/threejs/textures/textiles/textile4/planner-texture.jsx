import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'textile_4': {
                name : translator.t('Textile 4'),
                uri: require('./textile4.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#c6dd77'
            }   
        };
    },
};