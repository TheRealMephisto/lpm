import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PackageOptionsTreeviewComponent } from './package-options-treeview.component';

describe('PackageOptionsTreeviewComponent', () => {
  let component: PackageOptionsTreeviewComponent;
  let fixture: ComponentFixture<PackageOptionsTreeviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PackageOptionsTreeviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PackageOptionsTreeviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
