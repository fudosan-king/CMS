import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'switch_plate': {
                name : translator.t('Switch plate'),
                uri: require('./switch-plate.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#fbfafa'
            }   
        };
    },
};