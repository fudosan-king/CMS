import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'textile_2': {
                name : translator.t('Textile 2'),
                uri: require('./textile2.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#e7e1d6'
            }   
        };
    },
};