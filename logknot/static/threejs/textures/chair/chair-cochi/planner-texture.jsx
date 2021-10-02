import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'chair_cochi': {
                name : translator.t('Cushion'),
                uri: require('./cushion_bump.jpg'),
                lengthRepeatScale: 0.5,
                heightRepeatScale: 0.5,
                mesh : mesh,
                color: '#585858'
            }   
        };
    },
};