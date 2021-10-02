import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wall_stone_mosac': {
                name : translator.t('Stone mosac'),
                uri: require('./stone_mosaic.jpg'),
                lengthRepeatScale: 0.01,
                heightRepeatScale: 0.01,
                normalScaleX: 0.01,
                normalScaleY: 0.01,
                mesh : mesh,
                color:'#393837' 
            }   
        };
    },
};