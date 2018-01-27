title: Photoshop Script ps脚本相关资料收集
description: 
date: 2015-9-9
layout: post
comments: ture
categories:
- 笔记
tags: 
- Photoshop
---

最近做Label+ 顺便把js给入了门
后发现了xtools这个函数库 发现能做的事真的很多
xtools提供了便利的图形界面支持 实用标准函数集等等
有这些前人的积累 ps脚本就不必从零开始了

这里还是用来堆放一些函数

---

一篇不错的入门教程
http://www.uisdc.com/introduction-to-photoshop-scripting

官方文档集
http://www.adobe.com/devnet/photoshop/scripting.html

The ExtendScript Toolkit(与平台相关的File/Folder的资料在里边)
http://www.adobe.com/devnet/scripting/estk.html

xtools
http://ps-scripts.sourceforge.net/xtools.html

我写的xtools快速入门教程
http://noodlefighter.com/%E7%AC%94%E8%AE%B0/note_ps_script_xtools

"这个工具类似flatten 并且可以使用ES2015的一些语法" by SPecik
https://www.npmjs.com/package/extendscriptr

一个工具集 可以用于文字格式设置
https://github.com/tajmone/Tonton-Pixel-Photoshop-Scripts

---

来源列表

https://forums.adobe.com/message/4282351

---

## 图层操作

```
//START HERE------------------------------------------
//For code readability
function cTID(s){return charIDToTypeID(s)}
function sTID(s){return stringIDToTypeID(s)}
// =============================


function openAllLayerSets( parent ){
    for(var setIndex=0;setIndex<parent.layerSets.length;setIndex++){
        app.activeDocument.activeLayer = parent.layerSets[setIndex].layers[0];
        openAllLayerSets( parent.layerSets[setIndex]);
    }
};




function closeAllLayerSets(ref) {
          var layers = ref.layers;
          var len = layers.length;
          for ( var i = 0; i < len; i ++) {
                    var layer = layers[i];
                    if (layer.typename == 'LayerSet') {closeGroup(layer); var layer = layers[i]; closeAllLayerSets(layer);};
          }
}


function openGroup(layerSet) {
   var m_activeLayer = activeDocument.activeLayer;

   var m_Layer_Dummy01 = layerSet.artLayers.add();
   var m_Layer_Dummy02 = layerSet.artLayers.add();
   layerSet.layers[1].name = layerSet.layers[1].name;
   m_Layer_Dummy01.remove();
   m_Layer_Dummy02.remove();

   activeDocument.activeLayer = m_activeLayer;
}


function closeGroup(layerSet) {
   var m_Name = layerSet.name;
   var m_Opacity = layerSet.opacity;
   var m_BlendMode = layerSet.blendMode;
   var m_LinkedLayers = layerSet.linkedLayers;

   var m_bHasMask = hasLayerMask();
   if(m_bHasMask) loadSelectionOfMask();


   if(layerSet.layers.length <= 1) {
      addLayer();
      var m_Tmp = activeDocument.activeLayer;
      m_Tmp.name = "dummy - feel free to remove me";
      activeDocument.activeLayer = layerSet;
      ungroup();
      addToSelection("dummy - feel free to remove me");
      groupSelected(m_Name);

   } else {
      activeDocument.activeLayer = layerSet;
      ungroup();
      groupSelected(m_Name);
   }


   var m_Closed = activeDocument.activeLayer;
   m_Closed.opacity = m_Opacity;
   m_Closed.blendMode = m_BlendMode;

   for(x in m_LinkedLayers) {
      if(m_LinkedLayers[x].typename == "LayerSet")
         activeDocument.activeLayer.link(m_LinkedLayers[x]);
   }

   if(m_bHasMask) maskFromSelection();

   return m_Closed;
}


function ungroup() {
   var m_Dsc01 = new ActionDescriptor();
   var m_Ref01 = new ActionReference();
   m_Ref01.putEnumerated( cTID( "Lyr " ), cTID( "Ordn" ), cTID( "Trgt" ) );
   m_Dsc01.putReference( cTID( "null" ), m_Ref01 );

   try {
      executeAction( sTID( "ungroupLayersEvent" ), m_Dsc01, DialogModes.NO );
   } catch(e) {}
}


function addLayer() {
   var m_ActiveLayer          =    activeDocument.activeLayer;
   var m_NewLayer             =    activeDocument.artLayers.add();
   m_NewLayer.move(m_ActiveLayer, ElementPlacement.PLACEBEFORE);

   return m_NewLayer;
}


function hasLayerMask() {
   var m_Ref01 = new ActionReference();
   m_Ref01.putEnumerated( sTID( "layer" ), cTID( "Ordn" ), cTID( "Trgt" ));
   var m_Dsc01= executeActionGet( m_Ref01 );
   return m_Dsc01.hasKey(cTID('Usrs'));
}


function activateLayerMask() {
   var m_Dsc01 = new ActionDescriptor();
   var m_Ref01 = new ActionReference();
   m_Ref01.putEnumerated( cTID( "Chnl" ), cTID( "Chnl" ), cTID( "Msk " ) );
   m_Dsc01.putReference( cTID( "null" ), m_Ref01 );

   try {
      executeAction( cTID( "slct" ), m_Dsc01, DialogModes.NO );
   } catch(e) {
      var m_TmpAlpha = new TemporaryAlpha();

      maskFromSelection();
      activateLayerMask();

      m_TmpAlpha.consume();
   }
}


function deleteMask(makeSelection) {
   if(makeSelection) {
      loadSelectionOfMask();
   }

   var m_Dsc01 = new ActionDescriptor();
   var m_Ref01 = new ActionReference();
   m_Ref01.putEnumerated( cTID( "Chnl" ), cTID( "Ordn" ), cTID( "Trgt" ) );
   m_Dsc01.putReference( cTID( "null" ), m_Ref01 );

   try {
      executeAction( cTID( "Dlt " ), m_Dsc01, DialogModes.NO );
   } catch(e) {}
}


function selectLayerMask() {
   var m_Dsc01 = new ActionDescriptor();
   var m_Ref01 = new ActionReference();


   m_Ref01.putEnumerated(cTID("Chnl"), cTID("Chnl"), cTID("Msk "));
   m_Dsc01.putReference(cTID("null"), m_Ref01);
   m_Dsc01.putBoolean(cTID("MkVs"), false );


   try {
      executeAction(cTID("slct"), m_Dsc01, DialogModes.NO );
   } catch(e) {}
}


function loadSelectionOfMask() {
   selectLayerMask();

   var m_Dsc01 = new ActionDescriptor();
   var m_Ref01 = new ActionReference();
   m_Ref01.putProperty( cTID( "Chnl" ), cTID( "fsel" ) );
   m_Dsc01.putReference( cTID( "null" ), m_Ref01 );
   var m_Ref02 = new ActionReference();
   m_Ref02.putEnumerated( cTID( "Chnl" ), cTID( "Ordn" ), cTID( "Trgt" ) );
   m_Dsc01.putReference( cTID( "T   " ), m_Ref02 );

   try {
      executeAction( cTID( "setd" ), m_Dsc01, DialogModes.NO );
   } catch(e) {}
}


function maskFromSelection() {
   if(!hasLayerMask()) {
      var m_Dsc01 = new ActionDescriptor();
      m_Dsc01.putClass( cTID( "Nw  " ), cTID( "Chnl" ) );
      var m_Ref01 = new ActionReference();
      m_Ref01.putEnumerated( cTID( "Chnl" ), cTID( "Chnl" ), cTID( "Msk " ) );
      m_Dsc01.putReference( cTID( "At  " ), m_Ref01 );
      m_Dsc01.putEnumerated( cTID( "Usng" ), cTID( "UsrM" ), cTID( "RvlS" ) );

      try {
         executeAction( cTID( "Mk  " ), m_Dsc01, DialogModes.NO );
      } catch(e) {
         activeDocument.selection.selectAll();
         maskFromSelection();
      }
   } else {
      if(confirm("Delete existing mask?", true, "Warning")) {
         activateLayerMask();
         deleteMask();
      }
   }
}


function groupSelected(name) {
   var m_Dsc01 = new ActionDescriptor();
   var m_Ref01 = new ActionReference();
   m_Ref01.putClass( sTID( "layerSection" ) );
   m_Dsc01.putReference(  cTID( "null" ), m_Ref01 );
   var m_Ref02 = new ActionReference();
   m_Ref02.putEnumerated( cTID( "Lyr " ), cTID( "Ordn" ), cTID( "Trgt" ) );
   m_Dsc01.putReference( cTID( "From" ), m_Ref02 );
   var m_Dsc02 = new ActionDescriptor();
   m_Dsc02.putString( cTID( "Nm  " ), name);
   m_Dsc01.putObject( cTID( "Usng" ), sTID( "layerSection" ), m_Dsc02 );
   executeAction( cTID( "Mk  " ), m_Dsc01, DialogModes.NO );

   return activeDocument.activeLayer;
}


function addToSelection(layerName) {
   var m_Dsc01 = new ActionDescriptor();
   var m_Ref01 = new ActionReference();
   m_Ref01.putName( cTID( "Lyr " ), layerName );
   m_Dsc01.putReference( cTID( "null" ), m_Ref01 );
   m_Dsc01.putEnumerated( sTID( "selectionModifier" ), sTID( "selectionModifierType" ), sTID( "addToSelection" ) );
   m_Dsc01.putBoolean( cTID( "MkVs" ), false );

   try {
      executeAction( cTID( "slct" ), m_Dsc01, DialogModes.NO );
   } catch(e) {}
}


function TemporaryAlpha() {
   activeDocument.selection.store((this.alpha = activeDocument.channels.add()));
   activeDocument.selection.deselect();

   this.consume = function() {
      activeDocument.selection.load(this.alpha);
      this.alpha.remove();
   }
}


// The main function


//openGroup(activeDocument.activeLayer);
//openAllLayerSets( app.activeDocument );


//closeGroup(activeDocument.activeLayer);
//closeAllLayerSets( app.activeDocument );

//END HERE-----------------------------------------------
```

使用例子
```

//START HERE-----------------------------------------------
var doc = app.activeDocument;
var theLayer = activeDocument.activeLayer;
var theParent = theLayer.parent;
doc.activeLayer = theParent;
 

// =======================================================
 
// The main function
//@include "LayerSetSupport.jsx"


if (activeDocument.activeLayer.typename == 'LayerSet')
 
{app.activeDocument.suspendHistory('closeGroup','closeGroup
 
(activeDocument.activeLayer)');}
 
//END HERE-----------------------------------------------
```

---

