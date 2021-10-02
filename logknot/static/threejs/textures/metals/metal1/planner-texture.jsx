import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'metal_1': {
                name : translator.t('Metal') + ' 1',
                uri: require('./metal1.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#E2E2E2'
            }   
        };
    },
};