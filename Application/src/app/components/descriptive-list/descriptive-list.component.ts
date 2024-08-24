import { Component, OnInit, Input, OnChanges } from '@angular/core';

import { DescriptiveItem } from '../../model/descriptive-item';

@Component({
  selector: 'descriptive-list',
  templateUrl: './descriptive-list.component.html',
  styleUrls: ['./descriptive-list.component.scss']
})
export class DescriptiveListComponent implements OnInit, OnChanges {

  @Input() items: Array<DescriptiveItem>;

  constructor() { }

  ngOnInit() {}

  ngOnChanges() {}
}
