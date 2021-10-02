import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_kitchen_walnut': {
                name : translator.t('Wood Kitchen Walnut'),
                uri: require('./go-wanut.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#612405',
                hidden: true,
            }   
        };
    },
};