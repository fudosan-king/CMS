import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'arnica_sofa': {
                name : translator.t('Cushion'),
                uri: require('./sofa.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#0B0B3B'
            }   
        };
    },
};