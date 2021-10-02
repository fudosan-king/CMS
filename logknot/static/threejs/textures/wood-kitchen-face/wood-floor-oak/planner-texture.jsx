import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_floor_oak': {
                name : translator.t('Floor oak'),
                uri: require('./floor-oak.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#7F5111'
            }   
        };
    },
};