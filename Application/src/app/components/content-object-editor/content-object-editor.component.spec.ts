import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ContentObjectEditorComponent } from './content-object-editor.component';

describe('ContentObjectEditorComponent', () => {
  let component: ContentObjectEditorComponent;
  let fixture: ComponentFixture<ContentObjectEditorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ContentObjectEditorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ContentObjectEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
