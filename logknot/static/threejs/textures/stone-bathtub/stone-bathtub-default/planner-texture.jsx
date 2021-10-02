import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'bathtub_default': {
                name : translator.t('Ivory'),
                uri: require('./bathtub3.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#f3ead2'
            }   
        };
    },
};