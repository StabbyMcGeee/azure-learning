import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../data/local_store.dart';

/// Dropdown surface for selecting the active course.
///
/// Courses are discovered from the loaded content packs; the list is never
/// hardcoded. When no course is selected, every screen shows all available
/// content; selecting one scopes study, practice, exam, review, and progress
/// to that course.
class CourseSelector extends StatefulWidget {
  const CourseSelector({super.key});

  @override
  State<CourseSelector> createState() => _CourseSelectorState();
}

class _CourseSelectorState extends State<CourseSelector> {
  List<String> _courses = [];
  String? _selected;
  bool _loaded = false;

  LocalStore get _store => context.read<LocalStore>();

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final courses = await _store.getCourses();
    final selected = await _store.getSelectedCourseId();
    final effective =
        (selected != null && courses.contains(selected)) ? selected : null;
    if (selected != effective) {
      // The persisted selection no longer exists in the bank. Clear it so
      // the dropdown's displayed value and the stored value agree, and so
      // every screen falls back to "all courses" rather than filtering by a
      // vanished course id.
      await _store.setSelectedCourseId(null);
    }
    if (mounted) {
      setState(() {
        _courses = courses;
        _selected = effective;
        _loaded = true;
      });
    }
  }

  Future<void> _onChanged(String? courseId) async {
    if (courseId == _selected) return;
    await _store.setSelectedCourseId(courseId);
    if (mounted) {
      setState(() {
        _selected = courseId;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!_loaded) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_courses.isEmpty) {
      return const ListTile(
        leading: Icon(Icons.school_outlined),
        title: Text('No courses yet'),
        subtitle: Text(
          'This device has no course content yet. Update or reinstall the '
          'app to load your courses.',
        ),
      );
    }
    return DropdownButtonFormField<String?>(
      initialValue: _selected,
      decoration: const InputDecoration(
        labelText: 'Course',
        prefixIcon: Icon(Icons.school_outlined),
        border: OutlineInputBorder(),
      ),
      items: [
        const DropdownMenuItem<String?>(
          value: null,
          child: Text('All courses'),
        ),
        ..._courses.map((courseId) => DropdownMenuItem(
              value: courseId,
              child: Text(courseId),
            )),
      ],
      onChanged: _onChanged,
    );
  }
}
