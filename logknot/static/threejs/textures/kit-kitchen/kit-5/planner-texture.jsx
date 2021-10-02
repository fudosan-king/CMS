import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'kit_5': {
                name : translator.t('Kit') + '5',
                uri: require('./kit-5.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#F7F2EF'
            }   
        };
    },
};