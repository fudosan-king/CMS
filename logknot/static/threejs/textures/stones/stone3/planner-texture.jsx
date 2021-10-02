import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'stone_3': {
                name : translator.t('Stone' + '3'),
                uri: require('./stone_3.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#3d3b39'
            }   
        };
    },
};