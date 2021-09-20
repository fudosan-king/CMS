db.buildings.update({}, {
	$unset: {'price_full_renovation': 1, 'link_2d': 1, 'link_3d': 1, 'specification_description': 1}
});
