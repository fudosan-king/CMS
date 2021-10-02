import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'kit_3': {
                name : translator.t('Kit') + '3',
                uri: require('./kit-3.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#F7F2EF'
            }   
        };
    },
};