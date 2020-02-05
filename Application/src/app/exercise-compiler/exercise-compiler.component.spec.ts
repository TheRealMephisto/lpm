import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExerciseCompilerComponent } from './exercise-compiler.component';

describe('ExerciseCompilerComponent', () => {
  let component: ExerciseCompilerComponent;
  let fixture: ComponentFixture<ExerciseCompilerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExerciseCompilerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExerciseCompilerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
