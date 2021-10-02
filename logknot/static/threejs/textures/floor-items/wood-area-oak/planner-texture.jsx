import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_area_oak': {
                name : translator.t('Wood Area Oak'),
                uri: require('./wood.jpg'),
                lengthRepeatScale: 2,
                heightRepeatScale: 2,
                mesh : mesh,
                color: '#FAE330'
            }   
        };
    },
};